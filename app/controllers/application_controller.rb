require 'application_responder'

class ApplicationController < ActionController::Base
  Responders::FlashResponder.flash_keys = [:success, :failure]
  self.responder = ApplicationResponder
  respond_to :html

  protect_from_forgery with: :exception

  protected

  def user_is_admin
    return if current_user.try(:is_administrator?)

    flash[:danger] = "You don't have enough privileges for this action"
    redirect_to companies_path, status: :see_other
  end
end
