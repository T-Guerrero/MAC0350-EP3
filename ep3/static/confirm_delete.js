function onDeleteClick(url) {
  var decision = confirm(
    "Quer mesmo deletar? A informação será deletada permanentemente."
  );

  if (decision) {
    window.location.href = url;
  }
}
