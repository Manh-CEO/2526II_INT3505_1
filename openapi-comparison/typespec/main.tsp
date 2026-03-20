import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;
using TypeSpec.Rest;

@service({
  title: "Library Management API",
})
@server("http://localhost:5000", "Local server")
namespace Library {
  model Book {
    @key id: string;
    title: string;
    author: string;
    isbn: string;
  }

  model BookInput {
    title: string;
    author: string;
    isbn: string;
  }

  @route("/books")
  interface Books {
    @get list(): Book[];
    @post create(@body book: BookInput): Book;
  }

  @route("/books/{id}")
  interface BookDetails {
    @get read(@path id: string): Book | { @statusCode statusCode: 404, @body error: string };
  }
}
