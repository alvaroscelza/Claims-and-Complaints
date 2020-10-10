Rails.application.routes.draw do
  get '/users', to: 'users#index'
  patch '/users', to: 'users#update_administrators'
  resources :judgements
  resources :companies
  resources :businesses
  devise_for :users
  root 'companies#index'
end
