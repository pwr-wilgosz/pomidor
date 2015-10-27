List.destroy_all

10.times do |i|
  List.create(name: "List #{i}")
end
