class JudgementsController < ApplicationController
  before_action :set_judgement, only: %i[show edit update destroy]

  def index
    @judgements = Judgement.all
    respond_with(@judgements)
  end

  def show
    respond_with(@judgement)
  end

  def new
    @judgement = Judgement.new
    respond_with(@judgement)
  end

  def edit
  end

  def create
    @judgement = Judgement.new(judgement_params)
    @judgement.save
    respond_with(@judgement)
  end

  def update
    @judgement.update(judgement_params)
    respond_with(@judgement)
  end

  def destroy
    @judgement.destroy
    respond_with(@judgement)
  end

  private

  def set_judgement
    @judgement = Judgement.find(params[:id])
  end

  def judgement_params
    params.require(:judgement).permit(:opinion, :vote, :user, :company)
  end
end
