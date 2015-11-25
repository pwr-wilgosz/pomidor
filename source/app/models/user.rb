class User < ActiveRecord::Base
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable and :omniauthable
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :trackable, :validatable
  has_one :api_key
  has_many :lists, dependent: :destroy

  def self.find_by_access_token token
    if apikey = ApiKey.find_by(access_token: token)
      apikey.user
    end
  end

  def access_token
    api_key.present? ? api_key.access_token : nil
  end
end
