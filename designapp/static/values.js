$(document).ready(function(){
  $("#values").submit(function(){
    if (!$("#values input[name=liquid_flux]").val())
    {
      alert("missing liquid density");
      return false;
    }
    else if (!$("#values input[name=vapor_flux]").val())
    {
      alert("missing vapor density");
      return false;
    }
    else if (!$("#values input[name=liquid_density]").val())
     {
       alert("missing liquid density");
       return false;
    }
    else if (!$("#values input[name=vapor_density]").val())
    {
      alert("missing vapor_density");
      return false;
    }
    else if (!$("#values input[name=API]").val())
    {
      alert("missing API density");
      return false;
    }
    return true;
  })
})
