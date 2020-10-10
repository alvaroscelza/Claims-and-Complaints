Rails.application.routes.draw do
  resources :users
  resources :judgements
  resources :companies
  resources :businesses
  devise_for :users
  root 'companies#index'
end
