class RemoveRoleFromUser < ActiveRecord::Migration[5.1]
  def change
    remove_column :users, :role_id
    add_column :users, :is_admin, :boolean
  end
end
