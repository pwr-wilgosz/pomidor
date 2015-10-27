class ApplicationController < ActionController::Base
  protect_from_forgery with: :null_session

  respond_to :json

  def not_found
    render json: {msg: 'not_found'}
  end
end
