$("#show-cupcakes").click(getCupcakes);

async function getCupcakes() {
  const cupcakes = await axios.get("/api/cupcakes");
  let all_cupcakes = cupcakes.data.cupcakes;
  all_cupcakes.forEach((cupcake) => {
    console.log(cupcake.flavor);
    $("<ul>")
      .append($(`<li>${cupcake.flavor}</li>`))
      .appendTo($(".container"));
  });
}
