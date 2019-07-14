Rails.application.routes.draw do
  root 'static_pages#index'
  get '/static_pages/index'

  devise_for :users
  get '/users', to: 'users#index', as: :users
  patch '/users/update_administrators', to: 'users#update_administrators', as: :update_administrators
  resources :judgements
  resources :companies
  resources :businesses
  resources :permits
end
