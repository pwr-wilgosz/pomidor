class List < ActiveRecord::Base
  belongs_to :user
  has_many :tasks
  validates :name, presence: true


  def to_s
    name
  end
end

