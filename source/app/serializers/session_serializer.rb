class SessionSerializer < ApplicationSerializer
  attributes :name

  has_one :api_key, key: 'access_token'
end
