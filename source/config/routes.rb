Rails.application.routes.draw do
  resources :tasks
  devise_for :users
  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".

  # You can have the root of your site routed with "root"

  root 'lists#index'

  resources :lists

  get "/auth/:provider/callback" => "sessions#create"
  # get "/signout" => "sessions#destroy", :as => :signout

  # get "*path", to: 'application#not_found'
end
