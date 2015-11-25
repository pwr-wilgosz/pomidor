Rails.application.routes.draw do
  devise_for :users
  post '/login(.:format)', to: 'sessions#create'
  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".

  # You can have the root of your site routed with "root"

  devise_scope :user do
    authenticated :user do
      root 'lists#index', as: :root
    end

    unauthenticated do
      root 'devise/sessions#new', as: :unauthenticated_root
    end
  end

  resources :lists do
    resources :tasks
  end

  get "/sync", to: "application#sync"
  get "/auth/:provider/callback" => "sessions#create"
  # get "/signout" => "sessions#destroy", :as => :signout

  # get "*path", to: 'application#not_found'

end
