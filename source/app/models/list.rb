class List < ActiveRecord::Base
  belongs_to :user
  has_many :tasks, dependent: :destroy
  validates :name, presence: true

  include WithIdentifier

  def to_s
    name
  end
end

