Rails.application.routes.draw do
  root 'static_pages#index'
  get '/static_pages/index'

  devise_for resources :users
  resources :judgements
  resources :companies
  resources :businesses
  resources :permits
  resources :roles
end
