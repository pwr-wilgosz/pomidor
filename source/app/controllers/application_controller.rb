require "application_responder"

class ApplicationController < ActionController::Base
  self.responder = ApplicationResponder

  protect_from_forgery with: :null_session

  respond_to :html, :json

  # def not_found
  #   render json: {msg: 'not_found'}
  # end
end
