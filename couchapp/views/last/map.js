function(doc) {
  emit(doc.modified_at, [doc.title, doc.authors, doc.year]);
}