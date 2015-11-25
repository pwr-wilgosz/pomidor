class ListSerializer < ApplicationSerializer
  attributes :id, :name, :identifier, :created_at, :updated_at, :user_id

  belongs_to :user
  has_many :tasks
end
