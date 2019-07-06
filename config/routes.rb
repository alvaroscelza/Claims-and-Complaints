Rails.application.routes.draw do
  root 'static_pages#index'
  get '/static_pages/index'

  resources :judgements
  resources :users
  resources :companies
  resources :businesses
  resources :permits
  resources :roles
end
