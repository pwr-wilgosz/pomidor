class SessionsController < ApplicationController

  def create
    # user = User.find_by_provider_and_uid(auth["provider"], auth["uid"]) || User.create_with_omniauth(auth)
    # ApiKey.create(user_id: User.last.id) if user.api_key.nil?

    # render :json => user, serializer: SessionSerializer
  end

  def destroy
    ApiKey.find_by_access_token(params[:access_token]).destroy
  end
end
