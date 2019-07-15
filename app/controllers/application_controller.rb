require "application_responder"

class ApplicationController < ActionController::Base
  Responders::FlashResponder.flash_keys = [ :success, :failure ]
  self.responder = ApplicationResponder
  respond_to :html

  protect_from_forgery with: :exception
end
