import { useState, useEffect } from 'react';
import api from '../services/api';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '../components/ui/alert';
import { Loader2 } from 'lucide-react';

interface Plan {
  id: string;
  name: string;
  description: string;
  price: number;
  billing_cycle: string;
  features: Record<string, any>;
}

interface Subscription {
  id: string;
  status: string;
  start_date: string;
  end_date: string;
  plan: Plan;
}

const Subscriptions = () => {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [currentSubscription, setCurrentSubscription] = useState<Subscription | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [checkoutLoading, setCheckoutLoading] = useState<boolean>(false);
  // Remove unused navigate variable

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch available plans
        const plansResponse = await api.get('/plans');
        setPlans(plansResponse.data);
        
        // Fetch current subscription if exists
        try {
          const subscriptionResponse = await api.get('/subscriptions/current');
          setCurrentSubscription(subscriptionResponse.data);
        } catch (err: any) {
          // No active subscription, this is not an error
          if (err.response && err.response.status === 404) {
            setCurrentSubscription(null);
          } else {
            throw err;
          }
        }
      } catch (err: any) {
        console.error('Error fetching subscription data:', err);
        setError('Failed to load subscription information. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleSubscribe = async (planId: string) => {
    setCheckoutLoading(true);
    try {
      const response = await api.post('/create-checkout-session', { plan_id: planId });
      // Redirect to Stripe checkout
      window.location.href = response.data.checkout_url;
    } catch (err: any) {
      console.error('Error creating checkout session:', err);
      setError('Failed to initiate checkout. Please try again later.');
      setCheckoutLoading(false);
    }
  };

  const handleManageSubscription = async () => {
    setCheckoutLoading(true);
    try {
      const response = await api.post('/customer-portal');
      // Redirect to Stripe customer portal
      window.location.href = response.data.portal_url;
    } catch (err: any) {
      console.error('Error opening customer portal:', err);
      setError('Failed to open subscription management portal. Please try again later.');
      setCheckoutLoading(false);
    }
  };

  const handleCancelSubscription = async () => {
    if (!window.confirm('Are you sure you want to cancel your subscription? You will lose access to premium features at the end of your billing period.')) {
      return;
    }
    
    setCheckoutLoading(true);
    try {
      await api.delete('/subscriptions/current');
      setCurrentSubscription(prev => prev ? { ...prev, status: 'canceled' } : null);
      setError(null);
    } catch (err: any) {
      console.error('Error canceling subscription:', err);
      setError('Failed to cancel subscription. Please try again later.');
    } finally {
      setCheckoutLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-200px)]">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <span className="ml-2">Loading subscription information...</span>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Subscription Plans</h1>
      
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      
      {currentSubscription && (
        <div className="mb-8">
          <Card>
            <CardHeader>
              <CardTitle>Current Subscription</CardTitle>
              <CardDescription>
                Your current plan and subscription details
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="font-medium">Plan:</span>
                  <span>{currentSubscription.plan.name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Status:</span>
                  <span className={`capitalize ${
                    currentSubscription.status === 'active' 
                      ? 'text-green-600' 
                      : 'text-red-600'
                  }`}>
                    {currentSubscription.status}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Price:</span>
                  <span>${currentSubscription.plan.price}/month</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium">Start Date:</span>
                  <span>{new Date(currentSubscription.start_date).toLocaleDateString()}</span>
                </div>
                {currentSubscription.end_date && (
                  <div className="flex justify-between">
                    <span className="font-medium">Renewal Date:</span>
                    <span>{new Date(currentSubscription.end_date).toLocaleDateString()}</span>
                  </div>
                )}
              </div>
            </CardContent>
            <CardFooter className="flex justify-end space-x-2">
              {currentSubscription.status === 'active' && (
                <>
                  <Button 
                    variant="outline" 
                    onClick={handleManageSubscription}
                    disabled={checkoutLoading}
                  >
                    {checkoutLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                    Manage Subscription
                  </Button>
                  <Button 
                    variant="destructive" 
                    onClick={handleCancelSubscription}
                    disabled={checkoutLoading}
                  >
                    {checkoutLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                    Cancel Subscription
                  </Button>
                </>
              )}
            </CardFooter>
          </Card>
        </div>
      )}
      
      <div>
        <h2 className="text-2xl font-semibold mb-4">Available Plans</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map((plan) => (
            <Card key={plan.id} className={`${
              currentSubscription && currentSubscription.plan.id === plan.id
                ? 'border-primary border-2'
                : ''
            }`}>
              <CardHeader>
                <CardTitle>{plan.name}</CardTitle>
                <CardDescription>{plan.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="mb-4">
                  <span className="text-3xl font-bold">${plan.price}</span>
                  <span className="text-gray-500">/{plan.billing_cycle}</span>
                </div>
                <div className="space-y-2">
                  {Object.entries(plan.features).map(([key, value]) => (
                    <div key={key} className="flex items-start">
                      <div className="h-5 w-5 rounded-full bg-primary/20 flex items-center justify-center mr-2">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-3 w-3 text-primary">
                          <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                      </div>
                      <span className="text-sm">
                        {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}: {
                          Array.isArray(value) 
                            ? value.join(', ') 
                            : typeof value === 'boolean' 
                              ? value ? 'Yes' : 'No' 
                              : value
                        }
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
              <CardFooter>
                <Button 
                  className="w-full" 
                  onClick={() => handleSubscribe(plan.id)}
                  disabled={
                    checkoutLoading || 
                    (currentSubscription?.status === 'active' && currentSubscription.plan.id === plan.id)
                  }
                >
                  {checkoutLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                  {currentSubscription?.status === 'active' && currentSubscription.plan.id === plan.id
                    ? 'Current Plan'
                    : 'Subscribe'
                  }
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Subscriptions;
