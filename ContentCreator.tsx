import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Textarea } from '../components/ui/textarea';
import { Input } from '../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Label } from '../components/ui/label';

const ContentCreator = () => {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Create Content</h1>
      
      <Tabs defaultValue="social" className="w-full">
        <TabsList className="grid w-full grid-cols-3 mb-8">
          <TabsTrigger value="social">Social Media</TabsTrigger>
          <TabsTrigger value="email">Email</TabsTrigger>
          <TabsTrigger value="ad">Digital Ad</TabsTrigger>
        </TabsList>
        
        <TabsContent value="social" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Create Social Media Post</CardTitle>
              <CardDescription>
                Create engaging content for your social media platforms
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="platform">Platform</Label>
                <Select defaultValue="facebook">
                  <SelectTrigger>
                    <SelectValue placeholder="Select platform" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="facebook">Facebook</SelectItem>
                    <SelectItem value="instagram">Instagram</SelectItem>
                    <SelectItem value="twitter">Twitter</SelectItem>
                    <SelectItem value="linkedin">LinkedIn</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="headline">Headline</Label>
                <Input id="headline" placeholder="Enter an attention-grabbing headline" />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="content">Content</Label>
                <Textarea 
                  id="content" 
                  placeholder="Write your post content here..." 
                  className="min-h-[150px]"
                />
              </div>
              
              <div className="space-y-2">
                <Label>Media</Label>
                <div className="border-2 border-dashed rounded-md p-6 text-center">
                  <p className="text-sm text-gray-500 mb-2">Drag and drop an image here, or click to select</p>
                  <Button variant="outline" size="sm">Upload Image</Button>
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="tags">Tags</Label>
                <Input id="tags" placeholder="Enter tags separated by commas" />
              </div>
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline">Save as Draft</Button>
              <Button>Preview & Schedule</Button>
            </CardFooter>
          </Card>
        </TabsContent>
        
        <TabsContent value="email" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Create Email Campaign</CardTitle>
              <CardDescription>
                Design professional email content for your campaigns
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="subject">Subject Line</Label>
                <Input id="subject" placeholder="Enter email subject line" />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="preheader">Preheader</Label>
                <Input id="preheader" placeholder="Enter preheader text" />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email-content">Email Body</Label>
                <Textarea 
                  id="email-content" 
                  placeholder="Write your email content here..." 
                  className="min-h-[200px]"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="cta">Call to Action</Label>
                <Input id="cta" placeholder="e.g., Shop Now, Learn More, etc." />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="cta-url">CTA URL</Label>
                <Input id="cta-url" placeholder="https://your-website.com/landing-page" />
              </div>
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline">Save as Draft</Button>
              <Button>Preview & Send</Button>
            </CardFooter>
          </Card>
        </TabsContent>
        
        <TabsContent value="ad" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Create Digital Ad</CardTitle>
              <CardDescription>
                Design eye-catching ads for digital platforms
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="ad-type">Ad Type</Label>
                <Select defaultValue="display">
                  <SelectTrigger>
                    <SelectValue placeholder="Select ad type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="display">Display Ad</SelectItem>
                    <SelectItem value="social">Social Media Ad</SelectItem>
                    <SelectItem value="search">Search Ad</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="ad-headline">Headline</Label>
                <Input id="ad-headline" placeholder="Enter ad headline" />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="ad-description">Description</Label>
                <Textarea 
                  id="ad-description" 
                  placeholder="Write your ad description here..." 
                  className="min-h-[100px]"
                />
              </div>
              
              <div className="space-y-2">
                <Label>Ad Creative</Label>
                <div className="border-2 border-dashed rounded-md p-6 text-center">
                  <p className="text-sm text-gray-500 mb-2">Upload your ad creative</p>
                  <Button variant="outline" size="sm">Upload Image</Button>
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="ad-url">Destination URL</Label>
                <Input id="ad-url" placeholder="https://your-website.com/landing-page" />
              </div>
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline">Save as Draft</Button>
              <Button>Preview & Launch</Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ContentCreator;
