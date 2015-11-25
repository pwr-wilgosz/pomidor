class SessionsController < ApplicationController
  skip_before_action :restrict_access, only: :create

  def create
    user = User.find_by(email: params[:email])
    if user.present? && user.valid_password?(params[:password])
      set_flash_message(:notice, :signed_in) if is_flashing_format?
      sign_in(:user, user)
      user.create_api_key
      render json: { status: 200, access_token: user.access_token}
    else
      render json: { status: 403, message: "Invalid login or password" }
    end
  end

  def destroy
    ApiKey.find_by_access_token(params[:access_token]).destroy
  end

  def set_mapping
    @request.env["devise.mapping"] = Devise.mappings[:user]
  end
end
