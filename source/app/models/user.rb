class User < ActiveRecord::Base
  has_one :api_key
  has_many :lists
end
