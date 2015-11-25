class TaskSerializer < ActiveModel::Serializer
  attributes :id, :name, :list_id, :priority, :created_at, :updated_at, :identifier, :x, :y, :duration
  has_one :list
end
