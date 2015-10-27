require 'rails_helper'

RSpec.describe ListsController, type: :controller do
  let(:user) { create(:user) }
  before { user.create_api_key }

  describe "GET #index" do
    context "should return lists from first page" do
      before do
        5.times { user.lists.create(FactoryGirl.attributes_for(:list)) }
        get :index, access_token: "wrong_token", page: 1, per_page: 2, format: :json
      end

      it { expect(response.status).to eq 200 }
      it { expect(json['lists'].length).to eq 2 }
    end

    context "should return lists from second page" do
      before do
        5.times { user.lists.create(FactoryGirl.attributes_for(:list)) }
        get :index, access_token: "wrong_token", page: 2, per_page: 2, format: :json
      end

      it { expect(response.status).to eq 200 }
      it { expect(json['lists'].length).to eq 2 }
    end

    context "should return two lists in first page" do
      before do
        5.times { user.lists.create(FactoryGirl.attributes_for(:list)) }
        get :index, access_token: "wrong_token", page: 1, per_page: 2, format: :json
      end

      it { expect(response.status).to eq 200 }
      it { expect(json['lists'].count).to eq(2) }
    end

    context "should return three lists in first page" do
      before do
        5.times { user.lists.create(FactoryGirl.attributes_for(:list)) }
        get :index, access_token: "wrong_token", page: 1, per_page: 3, format: :json
      end

      it { expect(response.status).to eq 200 }
      it { expect(json['lists'].count).to eq(3) }
    end
  end

  describe "GET #show" do
    let(:list) { user.lists.create(FactoryGirl.attributes_for(:list)) }

    before do
      get :show, access_token: user.api_key.access_token, format: :json, id: list.id
    end

    it { expect(response.status).to eq 200 }
    it { expect(json["list"]["name"]).to eq(user.lists.first.name) }
  end

  # describe "POST #create"do
  #   context "with authorization" do
  #     context "with valid attributes" do
  #       it "creates a new list", pending: true  do
  #         expect{
  #           post :create, access_token: user.api_key.access_token, list: FactoryGirl.attributes_for(:list), format: :json
  #         }.to change(List, :count).by(1)
  #       end

  #       before do
  #         # post :create, access_token: user.api_key.access_token, list: FactoryGirl.attributes_for(:list), format: :json
  #       end

  #       it { expect(json["list"]["name"]).to eq(user.lists.first.name) }
  #     end

  #     context "with invalid attributes" do
  #       it "does not save the new list" do
  #         expect{
  #           post :create, access_token: user.api_key.access_token, list: {anchor: 'anchor'}, format: :json
  #         }.to_not change(List, :count)
  #       end
  #     end
  #   end

  #   context "without authorization" do
  #     it "creates a new list" do
  #       post :create, access_token: "wrong_token", list: FactoryGirl.attributes_for(:list), format: :json
  #       expect(response.status).to eq 401
  #     end
  #   end
  # end
end

