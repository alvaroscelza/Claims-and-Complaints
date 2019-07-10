module UsersHelper
  def user_is_admin?
    @user_role = current_user.role
    user_attributes = current_user.attributes
    user_role_id = user_attributes.role
    role = Role.find_by(id: user_role_id)
  end
end