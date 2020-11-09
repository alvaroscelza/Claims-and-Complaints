class JudgementsController < ApplicationController
  before_action :set_judgement, only: [:edit, :update, :destroy]
  before_action :authenticate_user!, except: [:index]
  before_action :check_permissions, only: [:edit, :update, :destroy]

  def new
    @company = Company.find(params[:company_id])
    @judgement = Judgement.new(company: @company)
    respond_with(@judgement.company)
  end

  def edit; end

  def create
    @judgement = Judgement.new(judgement_params)
    @judgement.company_id = params[:company_id]
    @judgement.user = current_user
    @judgement.save

    if @judgement.errors.any?
      respond_with(@judgement)
    else
      respond_with(@judgement.company)
    end
  end

  def update
    @judgement.update(judgement_params)
    respond_with(@judgement.company)
  end

  def destroy
    @judgement.destroy
    respond_with(@judgement.company)
  end

  private

  def set_judgement
    @judgement = Judgement.find(params[:id])
  end

  def check_permissions
    return if current_user.try(:is_administrator?) || @judgement.user == current_user

    flash[:danger] = "You don't have enough privileges for this action."
    redirect_to company_path(@judgement.company), status: :see_other
  end

  def judgement_params
    params.require(:judgement).permit(:opinion, :vote)
  end
end
