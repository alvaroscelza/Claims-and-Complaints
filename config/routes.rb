Rails.application.routes.draw do
  root 'welcome#index'

  devise_for :users
  get '/users', to: 'users#index'
  patch '/users', to: 'users#update_administrators'

  resources :companies do
    resources :judgements
  end
  resources :businesses
  resources :suggestions
end
