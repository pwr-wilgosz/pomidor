class TaskSerializer < ActiveModel::Serializer
  attributes :id, :name, :duration, :priority
  has_one :list
end
