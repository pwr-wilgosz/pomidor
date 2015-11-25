class List < ActiveRecord::Base
  belongs_to :user
  has_many :tasks, dependent: :destroy
  validates :name, presence: true

  REQUIRED_LIST_PARAMS = [:name, :updated_at, :identifier]

  include WithIdentifier

  def to_s
    name
  end

  class << self

    def valid_list(list_params)
      (REQUIRED_LIST_PARAMS - list_params.keys).empty?
    end

    def update_list list, list_params
      if list.updated_at < list_params[:updated_at]
        list.update_attributes(list_params.slice(*REQUIRED_LIST_PARAMS))
      end
    end


    def sync user, lists
      lists.each do |list_params|
        list_params.stringify_keys!

        tasks = list_params.delete("tasks")

        if valid_list(list_params)
          if (list = user.lists.find_by(identifier: list_params[:identifier])).present?

          update_list(list, list_params)

          else
            user.create_list(list_params.slice(*REQUIRED_LIST_PARAMS))
          end
        end

        Task.sync(list, tasks) if tasks
      end
    end
  end
end

