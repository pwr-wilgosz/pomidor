module WithIdentifier
  extend ActiveSupport::Concern

  included do
    after_save :set_identifier
  end

  IDENTIFIER_LENGTH = 8
  IDENTIFIER_BASE = [('a'..'z'), ('A'..'Z'), ('0'..'9')].map { |i| i.to_a }.flatten

  def klass
    self.class.base_class
  end

  module ClassMethods
    def generate_unique_identifier
      loop do
          ident = "serv-" + (1..IDENTIFIER_LENGTH).to_a.inject('') { |r| r + IDENTIFIER_BASE[rand(IDENTIFIER_BASE.length)] }
        break ident if self.base_class.where(identifier: ident).none?
      end
    end
  end

  private

  def set_identifier
    return if identifier.present?
    set_identifier!
  end

  def set_identifier!
    update_column :identifier, klass.generate_unique_identifier
  end

end
