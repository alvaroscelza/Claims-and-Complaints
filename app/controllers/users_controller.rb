class UsersController < ApplicationController
  before_action :admin_user

  def index
    @users = User.all
  end

  def update_administrators
    new_admins_emails = user_params
    User.find_each do |user|
      if new_admins_emails.include?(user.email)
        user.update(is_admin: true)
      else
        user.update(is_admin: false)
      end
    end
    respond_to do |format|
      format.html { redirect_to users_path, notice: 'Users were successfully updated.' }
      format.json { render users_path, status: :ok }
    end
  rescue Exception => ex
    format.html { redirect_to users_path, notice: ex.message }
    format.json { render json: ex.message, status: :unprocessable_entity }

  end

  private

  def user_params
    params.require(:admins)
  end
end
