require 'rails_helper'

RSpec.describe SessionsController, type: :controller do
  it 'should not get access token' do
    user = create :user, email: 'email@example.com', password: "password", password_confirmation: 'password'
    post :create, format: :json, email: 'email@example.com', password: 'pass'
    expect(json).to eq({"status" => 403, "message" => "Invalid login or password"})
  end

  it 'should get access token' do
    user = create :user, email: 'email@example.com', password: "password", password_confirmation: 'password'
        expect(user.access_token).to be_nil

    post :create, format: :json, email: 'email@example.com', password: 'password'

    expect(json).to eq({"status" => 200, "access_token" => user.reload.access_token})
  end

end
