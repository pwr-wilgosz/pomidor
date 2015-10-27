Rails.application.routes.draw do
  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".

  # You can have the root of your site routed with "root"

  root 'lists#index', defaults: { format: :json }


  resources :lists, only: [:index, :show, :update, :create], defaults: { format: :json }

  get "/auth/:provider/callback" => "sessions#create"
  get "/signout" => "sessions#destroy", :as => :signout

  get "*path", to: 'application#not_found'
end
