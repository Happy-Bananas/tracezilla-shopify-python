GET_PRODUCT_VARIANTS = """
query GetProductVariants($first: Int!, $after: String) {
  productVariants(first: $first, after: $after) {
    nodes { id sku displayName }
    pageInfo { hasNextPage endCursor }
  }
}
"""
