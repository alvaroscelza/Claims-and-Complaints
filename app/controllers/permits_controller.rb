class PermitsController < ApplicationController
  before_action :set_permit, only: [:show, :edit, :update, :destroy]

  respond_to :html

  def index
    @permits = Permit.all
    respond_with(@permits)
  end

  def show
    respond_with(@permit)
  end

  def new
    @permit = Permit.new
    respond_with(@permit)
  end

  def edit
  end

  def create
    @permit = Permit.new(permit_params)
    @permit.save
    respond_with(@permit)
  end

  def update
    @permit.update(permit_params)
    respond_with(@permit)
  end

  def destroy
    @permit.destroy
    respond_with(@permit)
  end

  private
    def set_permit
      @permit = Permit.find(params[:id])
    end

    def permit_params
      params.require(:permit).permit(:name, :needed_reputation)
    end
end
