from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
def generate_code(input_code: str) -> str:
    """
    Uses LangChain to generate a modified version of the given input code.

    Args:
        input_code (str): The original code to modify.

    Returns:
        str: The modified code.
    """
    # Define the prompt template
    prompt_template = PromptTemplate(
        input_variables=["code"],
        template=(
            """
            You are an AI programming assistant. Your task is to modify the given code snippet with the following requirements:

            1. Integrate GraphQL for CRUD operations using best practices.
            2. Ensure proper error handling and user feedback mechanisms.
            3. Include the necessary GraphQL queries and mutations.
            4. Keep the code clean and easy to understand.

            Input Code:
            ```python
            {code}
            ```

            Return the modified code in Python, ensuring it meets the specified requirements.
            """
        )
    )

    # Initialize the LangChain LLM
    llm = OpenAI(model="gpt-4", temperature=0)

    # Generate the modified code
    modified_code = llm.generate(
        prompt_template.format(code=input_code)
    )

    return modified_code

# Example usage
if __name__ == "__main__":
    # Replace this with the actual code you want to modify
    input_code = """
    // GraphQL client setup (add this to a utils or services folder)
import { ApolloClient, InMemoryCache, gql } from '@apollo/client';

export const client = new ApolloClient({
  uri: 'YOUR_GRAPHQL_ENDPOINT', // Replace with your endpoint
  cache: new InMemoryCache(),
});

// Queries and mutations
type Client = { id: string; client_name: string };
type Port = string;
type Product = string;
type Spec = string;

type EnquiryInput = {
  dateOfEnquiry: string;
  vesselName: string;
  imo?: string;
  client: string;
  trader: string;
  portOfSupply: string;
  dutyPaid: string;
  products: {
    name: string;
    specification: string;
    uomOfSupply: string;
    enquiryQuantityMin: number;
    enquiryQuantityMax: number;
  }[];
  notes?: string;
};

export const GET_CLIENTS = gql`
  query GetClients {
    clients {
      id
      client_name
    }
  }
`;

export const GET_PORTS = gql`
  query GetPorts {
    ports
  }
`;

export const GET_PRODUCTS = gql`
  query GetProducts {
    products
  }
`;

export const GET_SPECS = gql`
  query GetSpecs($product: String!) {
    specs(product: $product)
  }
`;

export const CREATE_ENQUIRY = gql`
  mutation CreateEnquiry($input: EnquiryInput!) {
    createEnquiry(input: $input) {
      id
      success
      message
    }
  }
`;

// Updated NewEnquiryForm component
import { useMutation, useQuery } from '@apollo/client';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { format } from 'date-fns';
import { ClientSearch } from './client-search';
import { ProductDialog } from './product-dialog';
import { SpecsDialog } from './specs-dialog';
import { PortOfSupplyDialog } from './port-of-supply-dialog';
import { Button, Input, Select, Textarea, Calendar, Popover } from '@/components/ui';
import { formSchema, type FormValues } from '@/lib/schema';

export function NewEnquiryForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      dateOfEnquiry: new Date(),
      products: [{ id: 1, uomOfSupply: "MT", enquiryQuantityMin: 200, enquiryQuantityMax: 250 }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'products',
  });

  const [createEnquiry, { loading: creatingEnquiry, error: createError }] = useMutation(CREATE_ENQUIRY);

  const onSubmit = async (data: FormValues) => {
    const formattedData = {
      ...data,
      dateOfEnquiry: format(data.dateOfEnquiry, 'yyyy-MM-dd'),
      products: data.products.map((p) => ({
        ...p,
        enquiryQuantityMin: parseFloat(p.enquiryQuantityMin),
        enquiryQuantityMax: parseFloat(p.enquiryQuantityMax),
      })),
    };
    try {
      const response = await createEnquiry({ variables: { input: formattedData } });
      alert(response.data.createEnquiry.message);
    } catch (err) {
      console.error('Error creating enquiry:', err);
    }
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <h2>New Enquiry</h2>
      <div>
        <label>Date of Enquiry</label>
        <Calendar selected={form.watch('dateOfEnquiry')} onChange={(date) => form.setValue('dateOfEnquiry', date)} />
      </div>
      <div>
        <label>Client</label>
        <ClientSearch onSelect={(client) => form.setValue('client', client)} />
      </div>
      <div>
        <label>Port of Supply</label>
        <PortOfSupplyDialog onSelect={(port) => form.setValue('portOfSupply', port)} />
      </div>
      {fields.map((field, index) => (
        <div key={field.id}>
          <ProductDialog onSelect={(product) => form.setValue(`products.${index}.name`, product)} />
          <SpecsDialog
            selectedProduct={form.watch(`products.${index}.name`)}
            onSelect={(spec) => form.setValue(`products.${index}.specification`, spec)}
          />
        </div>
      ))}
      <Button type="submit" disabled={creatingEnquiry}>Submit</Button>
      {createError && <p>Error: {createError.message}</p>}
    </form>
  );
}
    """

    # Generate the modified code
    modified_code = generate_code(input_code)

    # Print the modified code
    print("Modified Code:")
    print(modified_code)