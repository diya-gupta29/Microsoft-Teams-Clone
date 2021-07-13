(function () {
    var options = [];
    for (i = 0; i < ids.length; i++) {
      var option = "";
      
        option =
          "<input type = checkbox checked  value = " +
          ids[i] +
          " id = " +
          ids[i] +
          " name = checks >" +
          names[i] +
          "</input>";   
      options.push(option);
    }
    $("#team_members").append(options.join("<br>"));
  })();