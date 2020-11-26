class OwnableEntityController < ApplicationController
  protected

  def user_is_admin_or_entity_owner(entity)
    return if entity.user == current_user

    user_is_admin
  end
end
