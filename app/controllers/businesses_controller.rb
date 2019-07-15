class BusinessesController < ApplicationController
  before_action :set_business, only: [:show, :edit, :update, :destroy]

  respond_to :html

  def index
    @businesses = Business.all
    respond_with(@businesses)
  end

  def show
    respond_with(@business)
  end

  def new
    @business = Business.new
    respond_with(@business)
  end

  def edit
  end

  def create
    @business = Business.new(business_params)
    @business.save
    respond_with(@business)
  end

  def update
    @business.update(business_params)
    respond_with(@business)
  end

  def destroy
    @business.destroy
    respond_with(@business)
  end

  private
    def set_business
      @business = Business.find(params[:id])
    end

    def business_params
      params.require(:business).permit(:name)
    end
end
