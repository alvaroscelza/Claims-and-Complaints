Rails.application.routes.draw do
  root 'static_pages#index'
  get '/static_pages/index'

  devise_for :users
  get '/users', to: 'users#index', as: :users
  # get '/users/:id', to: 'users#show', as: :user
  # get '/users/new', to: 'users#new', as: :new_user
  # get '/users/edit', to: 'users#edit', as: :edit_user
  # post '/users', to: 'users#create', as: :create_user
  resources :judgements
  resources :companies
  resources :businesses
  resources :permits
end
