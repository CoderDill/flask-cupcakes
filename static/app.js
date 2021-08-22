async function getCupcakes() {
  const cupcakes = await axios.get("/api/cupcakes");
  let all_cupcakes = cupcakes.data.cupcakes;
  all_cupcakes.forEach((cupcake) => {
    $("#cupcakes")
      .append(
        $(`<li>${cupcake.flavor}</li>`).append(
          `<img src=${cupcake.image} width="125" height="125">`
        )
      )
      .appendTo($(".container"));
  });
}

getCupcakes();
