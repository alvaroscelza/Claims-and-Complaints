class UpdateJudgementFieldsValidations < ActiveRecord::Migration[5.1]
  def change
    change_column :judgements, :opinion, :string, null: false
    change_column :judgements, :user_id, :integer, null: false
    change_column :judgements, :company_id, :integer, null: false
    change_column :judgements, :vote, :boolean, null: false
  end
end
