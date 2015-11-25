require "application_responder"

class ApplicationController < ActionController::Base
  before_action :restrict_access
  before_action :authenticate_user!, unless: :api_request?
  self.responder = ApplicationResponder

  # protect_from_forgery with: :null_session

  respond_to :html, :json

  rescue_from CanCan::AccessDenied do |exception|
    respond_to do |format|
      format.html { redirect_to root_url, :alert => exception.message }
      format.json { render json: { status: 403, message: "You are not authorized to access this resource"} }
    end
  end

  def current_page
    (params[:page] || 1).to_i
  end

  def per_page
    (params[:per_page] || 10).to_i
  end

  def restrict_access
    if api_request? && ((token = params[:access_token]).blank? || (user = User.find_by_access_token(token).blank? ))
      render json: { status: 403, message: "You are not authorized to access this resource"}
    elsif (user = User.find_by_access_token(token)).present?
      sign_in(:user, user)
    end
  end
private

  def api_request?
    params[:format] == "json"
  end
end
