// GraphQL API service for Lancer Reserves
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const GRAPHQL_ENDPOINT = `${API_BASE_URL}/graphql`

/**
 * Execute a GraphQL query or mutation
 * @param {string} query - GraphQL query/mutation string
 * @param {object} variables - Variables for the query/mutation
 * @returns {Promise<any>} - GraphQL response data
 */
async function executeGraphQL(query, variables = {}) {
  try {
    const response = await fetch(GRAPHQL_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        variables,
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const result = await response.json()

    if (result.errors) {
      throw new Error(`GraphQL errors: ${result.errors.map(e => e.message).join(', ')}`)
    }

    return result.data
  } catch (error) {
    console.error('GraphQL request failed:', error)
    throw error
  }
}

// GraphQL Queries
const QUERIES = {
  RESERVES: `
    query Reserves($type: ReserveTypeEnum, $skip: Int, $limit: Int) {
      reserves(type: $type, skip: $skip, limit: $limit) {
        id
        name
        type
        label
        description
        bonuses {
          id
          val
        }
        deployables {
          name
          type
          size
          detail
        }
        actions {
          name
          activation
          detail
          range {
            type
            val
          }
          damage {
            type
            val
          }
        }
        synergies {
          locations
          detail
        }
        createdAt
        updatedAt
      }
    }
  `,
  
  RESERVE_BY_ID: `
    query Reserve($id: String!) {
      reserve(id: $id) {
        id
        name
        type
        label
        description
        bonuses {
          id
          val
        }
        deployables {
          name
          type
          size
          detail
        }
        actions {
          name
          activation
          detail
          range {
            type
            val
          }
          damage {
            type
            val
          }
        }
        synergies {
          locations
          detail
        }
        createdAt
        updatedAt
      }
    }
  `,
  
  RANDOM_RESERVES: `
    query RandomReserves($count: Int!, $type: ReserveTypeEnum) {
      randomReserves(count: $count, type: $type) {
        id
        name
        type
        label
        description
        createdAt
        updatedAt
      }
    }
  `,
  
  RESERVES_BY_LABEL: `
    query ReservesByLabel($label: String!) {
      reservesByLabel(label: $label) {
        id
        name
        type
        label
        description
        createdAt
        updatedAt
      }
    }
  `
}

// GraphQL Mutations
const MUTATIONS = {
  CREATE_RESERVE: `
    mutation CreateReserve($input: ReserveInput!) {
      createReserve(input: $input) {
        id
        name
        type
        label
        description
        bonuses {
          id
          val
        }
        deployables {
          name
          type
          size
          detail
        }
        actions {
          name
          activation
          detail
          range {
            type
            val
          }
          damage {
            type
            val
          }
        }
        synergies {
          locations
          detail
        }
        createdAt
        updatedAt
      }
    }
  `,
  
  UPDATE_RESERVE: `
    mutation UpdateReserve($id: String!, $input: ReserveUpdateInput!) {
      updateReserve(id: $id, input: $input) {
        id
        name
        type
        label
        description
        bonuses {
          id
          val
        }
        deployables {
          name
          type
          size
          detail
        }
        actions {
          name
          activation
          detail
          range {
            type
            val
          }
          damage {
            type
            val
          }
        }
        synergies {
          locations
          detail
        }
        createdAt
        updatedAt
      }
    }
  `,
  
  DELETE_RESERVE: `
    mutation DeleteReserve($id: String!) {
      deleteReserve(id: $id)
    }
  `
}

// API Functions
export const api = {
  /**
   * Fetch all reserves with optional filtering
   * @param {string} type - Reserve type filter (BONUS, RESOURCE, MECH, TACTICAL)
   * @param {number} skip - Number of records to skip
   * @param {number} limit - Maximum number of records to return
   * @returns {Promise<Array>} - Array of reserves
   */
  async fetchReserves(type = null, skip = 0, limit = 100) {
    const variables = { skip, limit }
    if (type) {
      variables.type = type
    }
    
    const data = await executeGraphQL(QUERIES.RESERVES, variables)
    return data.reserves
  },

  /**
   * Fetch a single reserve by ID
   * @param {string} id - Reserve ID
   * @returns {Promise<Object|null>} - Reserve object or null if not found
   */
  async fetchReserveById(id) {
    const data = await executeGraphQL(QUERIES.RESERVE_BY_ID, { id })
    return data.reserve
  },

  /**
   * Fetch random reserves
   * @param {number} count - Number of random reserves to fetch
   * @param {string} type - Optional type filter
   * @returns {Promise<Array>} - Array of random reserves
   */
  async fetchRandomReserves(count = 1, type = null) {
    const variables = { count }
    if (type) {
      variables.type = type
    }
    
    const data = await executeGraphQL(QUERIES.RANDOM_RESERVES, variables)
    return data.randomReserves
  },

  /**
   * Search reserves by label
   * @param {string} label - Label to search for
   * @returns {Promise<Array>} - Array of matching reserves
   */
  async fetchReservesByLabel(label) {
    const data = await executeGraphQL(QUERIES.RESERVES_BY_LABEL, { label })
    return data.reservesByLabel
  },

  /**
   * Create a new reserve
   * @param {Object} input - Reserve input data
   * @returns {Promise<Object>} - Created reserve
   */
  async createReserve(input) {
    const data = await executeGraphQL(MUTATIONS.CREATE_RESERVE, { input })
    return data.createReserve
  },

  /**
   * Update an existing reserve
   * @param {string} id - Reserve ID
   * @param {Object} input - Reserve update data
   * @returns {Promise<Object>} - Updated reserve
   */
  async updateReserve(id, input) {
    const data = await executeGraphQL(MUTATIONS.UPDATE_RESERVE, { id, input })
    return data.updateReserve
  },

  /**
   * Delete a reserve
   * @param {string} id - Reserve ID
   * @returns {Promise<boolean>} - Success status
   */
  async deleteReserve(id) {
    const data = await executeGraphQL(MUTATIONS.DELETE_RESERVE, { id })
    return data.deleteReserve
  }
}

// Reserve type constants
export const RESERVE_TYPES = {
  BONUS: 'Bonus',
  RESOURCE: 'Resource', 
  MECH: 'Mech',
  TACTICAL: 'Tactical'
}

// Helper function to generate unique IDs
export function generateReserveId() {
  return `reserve_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

// Helper function to format dates
export function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

export default api
