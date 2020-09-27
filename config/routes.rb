Rails.application.routes.draw do
  resources :judgements
  resources :companies
  resources :businesses
  root 'companies#index'
  devise_for :users
end
