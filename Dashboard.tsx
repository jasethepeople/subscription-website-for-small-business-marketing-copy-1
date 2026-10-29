import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const { user } = useAuth();
  
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardTitle>Content Created</CardTitle>
            <CardDescription>Your content creation statistics</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">0</div>
            <p className="text-sm text-gray-500 mt-2">Content items created this month</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Subscription Status</CardTitle>
            <CardDescription>Your current plan details</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-xl font-medium">
              {user?.subscription ? user.subscription.plan.name : 'No Active Plan'}
            </div>
            <Link to="/subscriptions">
              <Button variant="outline" className="mt-4 w-full">Manage Subscription</Button>
            </Link>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Common tasks and shortcuts</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            <Link to="/content/create">
              <Button className="w-full">Create New Content</Button>
            </Link>
            <Link to="/templates">
              <Button variant="outline" className="w-full">Browse Templates</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
      
      <div className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">Recent Content</h2>
        <Card>
          <CardContent className="p-6">
            <div className="text-center py-8">
              <p className="text-gray-500 mb-4">You haven't created any content yet.</p>
              <Link to="/content/create">
                <Button>Create Your First Content</Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
      
      <div>
        <h2 className="text-2xl font-semibold mb-4">Recommended Templates</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Social Media Post</CardTitle>
              <CardDescription>Perfect for Facebook and Instagram</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500 mb-4">Create engaging social media posts with customizable images and text.</p>
              <Link to="/templates">
                <Button variant="outline" className="w-full">Use Template</Button>
              </Link>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Email Newsletter</CardTitle>
              <CardDescription>Keep your customers informed</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500 mb-4">Professional email templates with sections for news, promotions, and updates.</p>
              <Link to="/templates">
                <Button variant="outline" className="w-full">Use Template</Button>
              </Link>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Special Promotion</CardTitle>
              <CardDescription>Drive sales with limited-time offers</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500 mb-4">Eye-catching promotional templates for special offers and discounts.</p>
              <Link to="/templates">
                <Button variant="outline" className="w-full">Use Template</Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
