(function () {
    var options = [];
    for (i = 0; i < ids.length; i++) {
      var option = "";
      // if user is admin or member of the team is the current user, then the user will be always checklisted
      if (admin[i] == 1 || ids[i] == user_id)
        option =
          "<input type = checkbox checked onclick = 'event.preventDefault()'  value=" +
          ids[i] +
          " id = " +
          ids[i] +
          " name = checks>" +
          names[i] +
          "</input>";
      else
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
  