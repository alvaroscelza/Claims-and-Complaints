Rails.application.routes.draw do
  root 'companies#index'

  devise_for :users
  get '/users', to: 'users#index', as: :users
  patch '/users/update_administrators', to: 'users#update_administrators', as: :update_administrators
  resources :companies do
    resources :judgements
  end
  resources :businesses
end
