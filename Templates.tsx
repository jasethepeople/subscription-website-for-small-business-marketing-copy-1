import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';

const Templates = () => {
  const navigate = useNavigate();
  
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Content Templates</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Product Showcase</CardTitle>
            <CardDescription>Highlight your products with style</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="aspect-video bg-gray-200 rounded-md mb-4 flex items-center justify-center">
              <span className="text-gray-500">Template Preview</span>
            </div>
            <p className="text-sm text-gray-500">Perfect for showcasing new products or services with a clean, professional layout.</p>
          </CardContent>
          <CardFooter>
            <Button className="w-full" onClick={() => navigate('/content/create')}>Use Template</Button>
          </CardFooter>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Customer Testimonial</CardTitle>
            <CardDescription>Build trust with real feedback</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="aspect-video bg-gray-200 rounded-md mb-4 flex items-center justify-center">
              <span className="text-gray-500">Template Preview</span>
            </div>
            <p className="text-sm text-gray-500">Share customer success stories and testimonials to build credibility.</p>
          </CardContent>
          <CardFooter>
            <Button className="w-full" onClick={() => navigate('/content/create')}>Use Template</Button>
          </CardFooter>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Special Promotion</CardTitle>
            <CardDescription>Drive engagement with offers</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="aspect-video bg-gray-200 rounded-md mb-4 flex items-center justify-center">
              <span className="text-gray-500">Template Preview</span>
            </div>
            <p className="text-sm text-gray-500">Announce sales, discounts, and special offers with eye-catching designs.</p>
          </CardContent>
          <CardFooter>
            <Button className="w-full" onClick={() => navigate('/content/create')}>Use Template</Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};

export default Templates;
